## Anisotropic exchange with Dzyaloshinskii-Moriya, Ising and Kitaev terms {#sec-6-12 number="6.12"}

In [(6.5)](#eq-6-5) we assumed that the coupling is an isotropic scalar product, $\mathbf S_i\cdot\mathbf
S_j$, which is what the rotational spin symmetry requires when there is no spin-orbit coupling. Once spin-orbit coupling is included in the underlying electronic Hamiltonian, other spin couplings with lower symmetry become allowed. Three of them appear often in real materials, and we list them now.

**Antisymmetric, or Dzyaloshinskii-Moriya, exchange**,
$$H_\text{DM} = \sum_{\langle ij\rangle} \mathbf D_{ij}\cdot\big(\mathbf S_i\times\mathbf S_j\big),$$
which is a cross product and not a dot product. It requires broken mirror symmetry, which is the reason why it is strong at surfaces and interfaces, where the substrate itself breaks this mirror symmetry. It favors neighboring spins rotated by roughly $90^\circ$ with respect to each other, so it favors noncollinear order, which is often a spiral.

**Anisotropic, or Ising-like, exchange**, which is a coupling of a single component such as $\Lambda\, S_i^z S_j^z$. It favors an easy axis, or an easy plane for the opposite sign, which means that the system magnetizes more easily along one direction than along another.

**Kitaev interaction**, which is a coupling that depends on the bond, on a lattice of honeycomb type. It has an $S^x_iS^x_j$ term on one bond direction, $S^y_iS^y_j$ on a second one and $S^z_iS^z_j$ on a third one,
$$H_\text{Kitaev} = \sum_{\langle ij\rangle \in x\text{-bonds}}\! K\, S_i^xS_j^x \;+\!\!\sum_{\langle ij\rangle \in y\text{-bonds}}\!\! K\, S_i^yS_j^y \;+\!\!\sum_{\langle ij\rangle \in z\text{-bonds}}\!\! K\, S_i^zS_j^z.$$
Even on a bipartite honeycomb lattice, where the geometry alone would not give any frustration, this dependence on the bond is frustrating by itself, since no single spin orientation can satisfy the three types of bonds at the same time (figure [6.4](#fig:s06:kitaev)). This interaction is what makes the Kitaev model a paradigm for quantum spin liquids, and this is why we point it out here explicitly, as an important preparation for the material on frustrated magnets in sessions 7 and 8.

![The Kitaev interaction and the second kind of frustration. The honeycomb lattice is bipartite, and its sites can be coloured with two colours, dark and light, as in figure [6.3](#fig:s06:frustration)(a). For this reason an ordinary Heisenberg antiferromagnet on this lattice is not frustrated at all. The Kitaev coupling gives frustration anyway, because each of the three bond directions, drawn in three styles, couples only *one* spin component. The $x$-bond only depends on $S^x$, so it favors both of its spins along $\pm\hat x$, the $y$-bond favors $\pm\hat y$, and the $z$-bond favors $\pm\hat z$. Every site belongs to one bond of each type, and no single orientation can satisfy three mutually orthogonal conditions at the same time, which the three ghost arrows on the highlighted site show. Here the frustration comes from the interaction and not from the geometry, and this is what makes the Kitaev model a paradigm for quantum spin liquids in sessions 7 and 8.](figures/s06f04_kitaev.svg){#fig:s06:kitaev number="6.4"}

::: notebookbox
**Notebook check-in:** [`session6.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session6.ipynb), "(Exercise) Non-collinear magnetism from spin-orbit coupling"

Add a term of Dzyaloshinskii-Moriya type to the mean-field Hamiltonian, and see how the ground state tilts away from collinear order. This is the electronic counterpart of the statement above for the spin model.
:::
