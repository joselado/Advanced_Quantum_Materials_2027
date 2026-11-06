## The mean-field spinon Hamiltonian and its dispersion classes {#sec-8-9 number="8.9"}

We put the couplings and the expectation value of [(8.14)](#eq-8-14) together into one mean-field parameter $\chi_{ij}$ per bond, and if needed we impose the constraint [(8.11)](#eq-8-11) on average with a Lagrange multiplier. In this way, the mean-field decoupling of Section [8.8](#sec-8-8) turns the original spin problem into a real Hamiltonian for the auxiliary fermions, which has the form of a tight-binding model and which we can diagonalize,

$$\mathcal H_\text{MF} = \sum_{ij,s} \chi_{ij}\, f^\dagger_{i,s} f_{j,s}. \tag{8.15}$$

This mean-field step is different from all the other mean-field decouplings of this course up to now, since it does not need to break time-reversal symmetry. If we take the same $\chi_{ij}$ for spin up and spin down, we keep $\langle \mathbf S_i\rangle = 0$ exactly, so the ground state that we obtain is time-reversal symmetric by construction, as [(8.5)](#eq-8-5) and [(8.9)](#eq-8-9) require. Equation [(8.15)](#eq-8-15) is a tight-binding model for the auxiliary fermions, with hoppings $\chi_{ij}$ that are fixed self-consistently by the geometry of the lattice and by the exchange couplings $J_{ij}$. Its excitations are the **spinons**, which are emergent fermionic quasiparticles with spin $1/2$ and no charge. We obtain them with the same procedure that we used for electrons in the whole course, which is to take a quartic interaction, decouple it at the mean-field level and diagonalize a bilinear Hamiltonian, and the only difference is that now we apply it to the spin sector. Figure [8.4](#fig:s08:parton)b shows the resulting picture, with spinons that hop on the lattice with amplitude $\chi_{ij}$, at half filling because of [(8.11)](#eq-8-11).

![What the Abrikosov-fermion rewriting [(8.10)](#eq-8-10) costs, and what it gives us. (a) The four fermionic states of a site. The two singly-occupied states give the physical spin-$1/2$ doublet exactly. The empty and doubly-occupied states, drawn as ghosts with a cross, are extra unphysical states, which [(8.10)](#eq-8-10) maps to $\mathbf S_i=\mathbf 0$ and which the constraint [(8.11)](#eq-8-11) removes by hand, and this constraint is the operator version of the Gutzwiller projector [(8.7)](#eq-8-7). (b) What remains after the mean-field decoupling [(8.14)](#eq-8-14), which is an ordinary tight-binding problem [(8.15)](#eq-8-15) for fermions with spin-$1/2$ and no charge, which hop with the self-consistent bond amplitude $\chi_{ij}$, drawn as the thickness of the bond, here with two values for illustration. Since there is one fermion per site, the resulting spinon model must be studied at half filling. Taking the same $\chi_{ij}$ for both spin species keeps $\langle\mathbf S_i\rangle=\mathbf 0$, so this mean field, unlike the magnetic mean fields of sessions 1 and 6, does not break time-reversal symmetry.](figures/s08f04_parton.svg){#fig:s08:parton number="8.4"}

When we diagonalize [(8.15)](#eq-8-15) on a given lattice, we obtain a real spinon band structure. Depending on the mean-field parameters that we obtain, there are three different possible outcomes.

- **Gapless spinons**, with excitations at energies as close to zero as we want.

- **Gapped spinons**, where it costs a finite energy to create a spinon.

- **Dirac spinons**, with a linear relation between energy and momentum at isolated points in the Brillouin zone.

::: notebookbox
**Notebook check-in:** [`session8.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session8.ipynb), "Spinon Fermi surface in gapless quantum spin liquids" (Core)

Build the spinon tight-binding Hamiltonian [(8.15)](#eq-8-15) on the triangular lattice and look at how its Fermi surface changes when the ratio of hopping amplitudes $t_2/t_1$ changes. In the quiz you repeat this on the square and kagome lattices, and you explain why the effective spinon model must be at half filling. The reason is the single-occupancy constraint [(8.11)](#eq-8-11) at the mean-field level.
:::

::: quiz
Why must the spinon tight-binding model [(8.15)](#eq-8-15) be studied at half filling?

- [x] There is one $f$ fermion on every site, which is the constraint [(8.11)](#eq-8-11) on average.
- [ ] The spinons have charge.
- [ ] The model has particle-hole symmetry only at half filling.
- [ ] A Fermi surface exists only at half filling.

Each site holds exactly one $f$ fermion, which is one particle for two spin states. This gives half filling of the spinon bands.
:::

::: quiz
We take the same $\chi_{ij}$ for spin up and spin down. What does this choice keep exact?

- [ ] The Fermi surface of the spinons.
- [x] $\langle\mathbf S_i\rangle=0$, so the state is time-reversal symmetric.
- [ ] The charge of the spinons.
- [ ] The value of the exchange coupling $J_{ij}$.

The two spin species see the same band, so no spin direction is selected. The state has zero magnetization by construction.
:::

::: {.tryit notebook="session8.ipynb" cell="Spinon Fermi surface in gapless quantum spin liquids"}
Change the values in `t2s` and look at how the spinon Fermi surface of the triangular lattice changes. Then replace `triangular_lattice` by `square_lattice` and see which shape the Fermi surface has at $t_2=0$ and half filling.
:::
