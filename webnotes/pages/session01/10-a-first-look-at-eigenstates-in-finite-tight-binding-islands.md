## A first look at eigenstates in finite tight-binding islands {#sec-1-10 number="1.10"}

Before we go to interactions, let us look at what a purely single-particle Hamiltonian already gives us, because this is something that we can compare directly with experiment. Let us take a tight-binding Hamiltonian $H = \sum_{ij} t_{ij}\, c_i^\dagger c_j$ on a honeycomb lattice, cut into a finite island that is triangular, hexagonal or rectangular, and let us diagonalize it. The probability density of a given eigenvector in real space can be compared directly with what a scanning tunneling microscope measures. Qualitatively, these states look like the finite-size states of a "particle in a box". The lowest-energy state has its maximum close to the center of the island, and the higher states have more and more nodes. This is a good first check, since single-particle diagonalization, with nothing more, already gives a structure that we can recognize and that we can measure in experiments.

::: notebookbox
**Notebook check-in:** [`session1.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session1.ipynb), "Finite sized chains" (Core), and "Density of states of a finite system as a function of the system size" (Challenge)

Diagonalize a finite chain or island, and look at how the spatial profiles of the eigenstates and the density of states change when you make the system larger. This is the numerical version of the particle-in-a-box argument above, and it is a good place to build intuition for how we approach an infinite periodic system, which we treat in session 2, starting from the finite-size case.
:::

We will use two software tools in all sessions. The first one is **PyQula**, which is a Python library for tight-binding and mean-field calculations, topological properties and spectral functions, and which we use through the Jupyter notebooks of the course. The second one is **Quantum Lattice**, which is a graphical interface built on PyQula that does not need any coding. Both are open source, and it is useful to have both open next to these notes.
