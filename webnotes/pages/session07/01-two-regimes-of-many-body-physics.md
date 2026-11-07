## Two regimes of many-body physics {#sec-7-1 number="7.1"}

Let us go back to the general interacting Hamiltonian that we have used in the whole course,

$$H = \sum_{ij} t_{ij}\, c_i^\dagger c_j \;+\; \sum_{ijkl} V_{ijkl}\, c_i^\dagger c_j c_k^\dagger c_l. \tag{7.1}$$

This is the Hamiltonian [(1.5)](#eq-1-5) of Session 1 with the four operators in another order, which only relabels $V_{ijkl}$ and adds a bilinear term to the hopping. The kinetic term is free and can be solved exactly, and the interaction term in general cannot. In all sessions so far we treated [(7.1)](#eq-7-1) in the same way. We decoupled the quartic term with mean field, as in Section [1.12](#sec-1-12), we replaced it with an effective bilinear Hamiltonian, and we looked at which symmetry is broken by the resulting order parameter. This strategy defines what we can call **weakly correlated matter**. In this sense, the magnets of Session 6, the superconductors of Session 5 and the charge density wave of Section [1.13](#sec-1-13) are all single-particle physics, once we find the right symmetry-broken background.

In this session we are in the opposite regime, which is **strongly correlated matter**. Here the interactions are so strong that no effective single-particle Hamiltonian gives the ground state, for any choice of the decoupling. Quantum spin liquids and fractional Chern insulators are our two main examples, and more generally, the same problem appears when we want an accurate phase diagram of a truly interacting model. In both cases we cannot solve the problem with an ansatz for the broken symmetry. Instead, we need something close to an exact numerical solution, or at least a controlled approximation that does not assume symmetry breaking from the start. This is what tensor networks give us.

::: quiz
A quantum spin liquid has no order parameter. What does a self-consistent mean-field calculation give for it?

- [ ] A small but finite magnetization that grows with the system size.

    This is false. A finite magnetization is a magnetic order, and a spin liquid has none. For the singlet of two spins we find $\langle S^z_i\rangle=0$ exactly, at every size.

- [x] A zero order parameter, which tells us nothing about the true ground state.

    This is true. The self-consistent loop looks for a symmetry-broken solution. If the true state has none, the loop converges to zero, which is a valid but empty answer.

- [ ] The exact ground state energy, but not the wave function.

    This is false. Mean field is a product-like trial state, so its energy is only an upper bound. For the singlet of two spins the best mean-field energy is $-1/4$ while the exact one is $-3/4$.

    ![Two spins in a product state against the singlet. The best product state has the energy $-\frac14$ and the singlet has $-\frac34$.](figures/web/session07/singlet_vs_product.svg){alt="The energy of two spins in a product state against the angle between them, with a minimum of minus one quarter, and a dashed line for the singlet at minus three quarters."}

:::

## Fermions and spins, two languages for the same physics {#sec-7-2 number="7.2a"}

Before we build the tool, let us point out something that was present in the last sessions without being said explicitly. We have used two families of many-body Hamiltonians that look different. The first family is the fermionic Hamiltonians of the form [(7.1)](#eq-7-1), with a general two-body interaction $V_{ijkl}$, where density-density interactions are only a special case, and we used them in Sessions 1 to 5. The second family is the spin Hamiltonians, mainly the Heisenberg model $H =
\sum_{ij} J_{ij}\, \mathbf{S}_i \cdot \mathbf{S}_j$ of [(6.5)](#eq-6-5). We used it for the magnons of Section [6.13](#sec-6-13), and we use it again in this session for quantum spin liquids. These are not two different topics. They are the same physics written in two different languages, and in this section we make this translation precise.

![On one site the fermion and the spin-1/2 are the same object, since an empty site is a down spin and an occupied site is an up spin. Between two sites the two languages differ in one sign, because fermion operators anticommute and spin operators commute. Look at the right side of the figure, since this is the sign that the string of the next section has to carry.](figures/web/session07/two_languages.svg){#sch:s07:two_languages alt="Three sites drawn as fermions, empty or full, above the same three sites drawn as spin arrows, with the rules of anticommutation and commutation at the right."}

::: quiz
We replace $c_1^\dagger$ and $c_2^\dagger$ of two different sites by $S_1^+$ and $S_2^+$ with no extra factor. What goes wrong?

- [ ] The operator $S^z_i=n_i-\tfrac12$ gets the wrong sign.

    This is false. On one site $S^z=n-\tfrac12$ is exact, since an occupied site is $S^z=+1/2$ and an empty site is $-1/2$. The problem only appears between two sites.

- [x] The spin operators commute while the fermion operators anticommute, so the relative sign between sites is wrong.

    This is true. On a single site the replacement is exact, as the figure shows. Between two sites the commutator and the anticommutator differ, and this is the sign that the Jordan-Wigner string will carry.

- [ ] The resulting Hamiltonian is no longer Hermitian.

    This is false. The hopping term $c_1^\dagger c_2+c_2^\dagger c_1$ is replaced by $S_1^+S_2^-+S_2^+S_1^-$, which is its own Hermitian conjugate. The Hamiltonian stays Hermitian and it is just the wrong one.
:::

::: comesback
- In Section [7.2b](#sec-7-2b) the Jordan-Wigner string fixes the sign between sites, and the two languages become one exact mapping.
- In Section [8.3](#sec-8-3) the singlet of two spins is the starting point of quantum magnetism, and in Section [8.9](#sec-8-9) mean field comes back for spinons without breaking any symmetry.
- In Section [10.3](#sec-10-3) neural network quantum states are a second tool for the strongly correlated regime.
:::
