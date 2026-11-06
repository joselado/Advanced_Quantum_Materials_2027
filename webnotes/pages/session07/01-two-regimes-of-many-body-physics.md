## Two regimes of many-body physics {#sec-7-1 number="7.1"}

Let us go back to the general interacting Hamiltonian that we have used in the whole course,

$$H = \sum_{ij} t_{ij}\, c_i^\dagger c_j \;+\; \sum_{ijkl} V_{ijkl}\, c_i^\dagger c_j c_k^\dagger c_l. \tag{7.1}$$

The kinetic term is free and can be solved exactly, and the interaction term in general cannot. In all sessions so far we treated [(7.1)](#eq-7-1) in the same way. We decoupled the quartic term with mean field, we replaced it with an effective bilinear Hamiltonian, and we looked at which symmetry is broken by the resulting order parameter. This strategy defines what we can call **weakly correlated matter**. In this sense, magnets, superconductors and charge density waves are all single-particle physics, once we find the right symmetry-broken background.

In this session we are in the opposite regime, which is **strongly correlated matter**. Here the interactions are so strong that no effective single-particle Hamiltonian gives the ground state, for any choice of the decoupling. Quantum spin liquids and fractional Chern insulators are our two main examples, and more generally, the same problem appears when we want an accurate phase diagram of a truly interacting model. In both cases we cannot solve the problem with an ansatz for the broken symmetry. Instead, we need something close to an exact numerical solution, or at least a controlled approximation that does not assume symmetry breaking from the start. This is what tensor networks give us.
