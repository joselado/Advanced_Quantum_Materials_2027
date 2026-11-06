## The resonating valence bond wavefunction as the QSL ground state {#sec-8-6 number="8.6"}

For a frustrated Heisenberg Hamiltonian $\mathcal H = \sum_{ij} J_{ij}\, \mathbf
S_i\cdot\mathbf S_j$, we do not expect the ground state to be one fixed dimer covering as in [(8.5)](#eq-8-5). Instead, we expect a **linear combination of singlets over every possible pairing of sites**, where each pairing has its own amplitude, which is a complicated many-body wavefunction. We could try to treat this directly, for example by writing it as a tensor network as in Session 7 for the general strongly correlated case. There is, however, a way that is easier to understand physically, which is a variational ansatz based on an analogy with superconductivity.

The idea is that the singlets in a QSL are similar to the Cooper pairs in an s-wave superconductor, since both are singlet correlations between pairs. A BCS-type wavefunction is easy to write at the mean-field level in the right basis, which is the Nambu space as in Session 5. So we start from a BCS-paired state built from the same auxiliary fermions $f_{i\sigma}$ that we will justify in detail in Section [8.8](#sec-8-8),

$$|\Psi_\text{BCS}\rangle = \prod_{\mathbf k}\Big(u_{\mathbf k} + v_{\mathbf k}\,
f^\dagger_{\mathbf k\uparrow} f^\dagger_{-\mathbf k\downarrow}\Big)|0\rangle, \tag{8.6}$$

where $u_{\mathbf k}, v_{\mathbf k}$ are variational parameters, as in the BCS state of Session 5. By itself, [(8.6)](#eq-8-6) is a superposition of states with every possible number of fermions per site, which can be empty, singly occupied or doubly occupied. This is not a physical spin state at all. A QSL has strong local interactions, so we need single occupation on every site, and no charge fluctuations between sites are allowed. We impose this condition with a **Gutzwiller projector** onto the singly-occupied subspace,

$$|\Psi_\text{RVB}\rangle = P_G\,|\Psi_\text{BCS}\rangle, \qquad P_G = \prod_i n_i(2-n_i), \qquad
n_i = \sum_\sigma f^\dagger_{i\sigma}f_{i\sigma}, \tag{8.7}$$

which gives $1$ for states with exactly one fermion per site and $0$ for all other states. What remains is a real many-body spin wavefunction. It is a superposition over the different ways to pair sites into singlets, in the same spirit as the singlet of a single dimer [(8.3)](#eq-8-3), but now over a whole frustrated lattice. The name of this construction describes what it is, and it is called the **resonating valence bond (RVB)** variational wavefunction. It turns out to be a good description of the physics of quantum spin liquids. Figure [8.3](#fig:s08:vbsrvb) shows what makes this resonating state, and the excitations that it has, different from the frozen dimer covering of Section [8.5](#sec-8-5).

![The difference between a valence bond solid and a quantum spin liquid is not whether the ground state is built from singlets, since both are, but whether the singlet pattern is frozen. (a1) The fully dimerized model [(8.4)](#eq-8-4) has one fixed covering, [(8.5)](#eq-8-5). (a2) When we separate the two unpaired spins of figure [8.1](#fig:s08:magnonspinon)b, every strong bond between them loses its singlet, drawn in red, so the energy cost grows with the separation. The pair is confined, and only the bound object propagates, which is the spin-$1$ triplon. (b1) The RVB state [(8.7)](#eq-8-7) is a superposition over *all* pairings, near and far, drawn as coverings stacked on top of each other. (b2) Now the background pairs again behind the excitations with no cost, the confining string does not form, and the two halves separate as independent spin-$1/2$ spinons. Frustration is the reason why the superposition in (b1), and not a single covering, is the ground state.](figures/s08f03_vbs_rvb.svg){#fig:s08:vbsrvb number="8.3"}

::: quiz
Why do we apply the Gutzwiller projector $P_G$ to the BCS state [(8.6)](#eq-8-6)?

- [ ] The BCS state is not normalized.
- [x] The BCS state has empty and doubly occupied sites, and a spin state needs exactly one fermion on every site.
- [ ] The BCS state breaks spin-rotation symmetry.
- [ ] The projector makes the state a superconductor.

In the BCS state the number of fermions on a site fluctuates between zero and two. Projecting onto single occupancy leaves only the spin degrees of freedom.
:::

::: quiz
We separate the two spinons that come from breaking a singlet. In which state does the energy cost grow with the separation?

- [x] In the valence bond solid, since every singlet between the two is broken.
- [ ] In the RVB state, since the singlets are frozen.
- [ ] In both states in the same way.
- [ ] In neither, since spinons always cost the same energy.

In the frozen covering the broken singlets between the spinons form a string, and the spinons are confined into a triplon. In the RVB state the background pairs again, so the spinons separate freely.
:::

::: {.tryit notebook="session8.ipynb" cell="Magnetization of a large Heisenberg model with a magnetic impurity"}
Run the chain with a local field on site 0 and look at the magnetization along the chain. It should alternate in sign from site to site and decay slowly, as in a critical state. Compare with the dimerized chain of the previous section.
:::
