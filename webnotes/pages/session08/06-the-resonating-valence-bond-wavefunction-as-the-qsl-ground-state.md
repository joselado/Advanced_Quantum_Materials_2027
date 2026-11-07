## The resonating valence bond wavefunction as the QSL ground state {#sec-8-6 number="8.6"}

For a frustrated Heisenberg Hamiltonian $\mathcal H = \sum_{ij} J_{ij}\, \mathbf
S_i\cdot\mathbf S_j$, we do not expect the ground state to be one fixed dimer covering as in [(8.5)](#eq-8-5). Instead, we expect a **linear combination of singlets over every possible pairing of sites**, where each pairing has its own amplitude, which is a complicated many-body wavefunction. We could try to treat this directly, for example by writing it as a tensor network, as in Section [7.4](#sec-7-4) for the general strongly correlated case. There is, however, a way that is easier to understand physically, which is a variational ansatz based on an analogy with superconductivity.

The idea is that the singlets in a QSL are similar to the Cooper pairs in an s-wave superconductor, since both are singlet correlations between pairs. A BCS-type wavefunction is easy to write at the mean-field level in the right basis, which is the Nambu space of Section [5.8](#sec-5-8). So we start from a BCS-paired state built from the same auxiliary fermions $f_{i\sigma}$ that we will justify in detail in Section [8.8](#sec-8-8),

$$|\Psi_\text{BCS}\rangle = \prod_{\mathbf k}\Big(u_{\mathbf k} + v_{\mathbf k}\,
f^\dagger_{\mathbf k\uparrow} f^\dagger_{-\mathbf k\downarrow}\Big)|0\rangle, \tag{8.6}$$

where $u_{\mathbf k}, v_{\mathbf k}$ are variational parameters, the coherence factors of a BCS state. This is the ground state of the mean-field pairing Hamiltonian of Section [5.5](#sec-5-5), and the Bogoliubov-de Gennes Hamiltonian of Section [5.8](#sec-5-8) gives the same factors as its eigenvectors. By itself, [(8.6)](#eq-8-6) is a superposition of states with every possible number of fermions per site, which can be empty, singly occupied or doubly occupied. This is not a physical spin state at all. A QSL has strong local interactions, so we need single occupation on every site, and no charge fluctuations between sites are allowed. We impose this condition with a **Gutzwiller projector** onto the singly-occupied subspace,

$$|\Psi_\text{RVB}\rangle = P_G\,|\Psi_\text{BCS}\rangle, \qquad P_G = \prod_i n_i(2-n_i), \qquad
n_i = \sum_\sigma f^\dagger_{i\sigma}f_{i\sigma}, \tag{8.7}$$

which gives $1$ for states with exactly one fermion per site and $0$ for all other states. What remains is a real many-body spin wavefunction. It is a superposition over the different ways to pair sites into singlets, in the same spirit as the singlet of a single dimer [(8.3)](#eq-8-3), but now over a whole frustrated lattice. The name of this construction describes what it is, and it is called the **resonating valence bond (RVB)** variational wavefunction. It turns out to be a good description of the physics of quantum spin liquids. Figure [8.3](#fig:s08:vbsrvb) shows what makes this resonating state, and the excitations that it has, different from the frozen dimer covering of Section [8.5](#sec-8-5).

![The difference between a valence bond solid and a quantum spin liquid is not whether the ground state is built from singlets, since both are, but whether the singlet pattern is frozen. (a1) The fully dimerized model [(8.4)](#eq-8-4) has one fixed covering, [(8.5)](#eq-8-5). (a2) When we separate the two unpaired spins of Figure [8.1](#fig:s08:magnonspinon)b, every strong bond between them loses its singlet, drawn in red, so the energy cost grows with the separation. The pair is confined, and only the bound object propagates, which is the spin-$1$ triplon. (b1) The RVB state [(8.7)](#eq-8-7) is a superposition over *all* pairings, near and far, drawn as coverings stacked on top of each other. (b2) Now the background pairs again behind the excitations with no cost, the confining string does not form, and the two halves separate as independent spin-$1/2$ spinons. Frustration is the reason why the superposition in (b1), and not a single covering, is the ground state.](figures/s08f03_vbs_rvb.svg){#fig:s08:vbsrvb number="8.3"}

![Why resonance lowers the energy, on the smallest example. A plaquette of four spins with the Heisenberg coupling $J$ on its four bonds has two singlet coverings, $|a\rangle$ and $|b\rangle$, each made of two singlets [(8.3)](#eq-8-3). We compute the energy of $\cos\theta|a\rangle+\sin\theta|b\rangle$. A single covering gives $-\tfrac32 J$, since only its two covered bonds gain energy. The equal superposition at $\theta=\pi/4$ gives $-2J$, which is the exact ground state of the plaquette. The other combination, $|a\rangle-|b\rangle$, is an excited singlet at zero energy. The RVB state [(8.7)](#eq-8-7) is this resonance over all the coverings of a lattice.](figures/web/session08/rvb_plaquette.svg){#sch:s08:rvb_plaquette alt="The energy against the mixing angle of two singlet coverings of a square of four sites, equal to minus three halves for a single covering, with a minimum of minus two at pi over four, and small drawings of the coverings."}

::: quiz
Why do we apply the Gutzwiller projector $P_G$ to the BCS state [(8.6)](#eq-8-6)?

- [ ] The BCS state breaks spin-rotation symmetry.

    This is false. The singlet pairing $\Delta(c^\dagger_\uparrow c^\dagger_\downarrow-c^\dagger_\downarrow c^\dagger_\uparrow)$ has total spin zero, and it is invariant under spin rotations. The projector is not needed for this.

- [x] The BCS state has empty and doubly occupied sites, and a spin state needs exactly one fermion on every site.

    This is true. In the BCS state of [(8.6)](#eq-8-6) the number of fermions on a site fluctuates between zero and two. Projecting onto single occupancy leaves only the spin degrees of freedom.

    ![Look at the two crossed states, the empty and the doubly occupied one.](figures/s08f04_parton.svg){alt="The four fermionic states of one site, with the two singly occupied states as the spin doublet and the other two crossed out."}

- [ ] The projector makes the state a superconductor.

    This is false. With exactly one fermion on each site the charge cannot move or fluctuate, so the projected state is a Mott insulator. The projection removes the charge degrees of freedom.
:::

::: quiz
We separate the two spinons that come from breaking a singlet. In which state does the energy cost grow with the separation?

- [x] In the valence bond solid, since every singlet between the two is broken.

    This is true. In the frozen covering the broken singlets between the spinons form a string, and the spinons are confined into a triplon. In the RVB state the background pairs again, so the spinons separate freely.

- [ ] In the RVB state, since the singlets are frozen.

    This is false. The RVB state is a superposition of many coverings, so no pattern is frozen. Moving a spinon by two sites only re-pairs the singlets along its path and leaves no string behind.

- [ ] In both states in the same way.

    This is false. In a dimerized chain a spinon pair at distance $d$ leaves about $d/2$ broken singlets and costs an energy proportional to $d$. In the RVB state the cost does not depend on $d$.
:::

::: {.tryit notebook="session8.ipynb" cell="Magnetization of a large Heisenberg model with a magnetic impurity"}
Run the chain with a local field on site 0 and look at the magnetization along the chain. It should alternate in sign from site to site and decay slowly, as in a critical state. Compare with the dimerized chain of the previous section.
:::

::: comesback
- In Section [8.8](#sec-8-8) the auxiliary fermions $f_{i\sigma}$ of [(8.6)](#eq-8-6) are justified as Abrikosov fermions, and the single-occupancy constraint is the operator form of $P_G$.
- In Section [8.9](#sec-8-9) the mean-field spinon Hamiltonian keeps the state time-reversal symmetric, as the RVB state is.
- In Section [9.9](#sec-9-9) a ground state similar to a spin liquid responds to a local magnetic impurity.
:::
