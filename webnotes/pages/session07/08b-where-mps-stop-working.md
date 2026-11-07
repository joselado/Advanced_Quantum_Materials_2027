## Where MPS stop working {#sec-7-8b number="7.8b"}

The same argument tells us directly where MPS must fail, which is whenever the true entanglement entropy is larger than what a practical bond dimension can give through [(7.10)](#eq-7-10). In practice this happens in four cases. The first case is dynamics over long times, since after a quench the entanglement grows *linearly* with time and not logarithmically, as [](#sch:s07:quench_entropy) shows for a small chain. The second case is systems in more than one dimension. There the length of the boundary in the area law grows with the system size, as we saw in Section [7.7](#sec-7-7). So $M$ has to grow too, often exponentially in the linear size of the subsystem. The third case is highly excited states, since the area law is a statement about ground states and not about general eigenstates. The fourth case is, more generally, states far from equilibrium. However, when the physics stays close to a gapped 1D ground state, MPS can be used for more than the ground-state problem. With a higher cost, they can be used for time evolution, excited states and open quantum systems, routinely in 1D and in some cases in 2D.

![The entropy of half of a transverse-field Ising chain with 12 sites after a quench, from exact time evolution. The chain starts with all spins up along $z$ and evolves with $H=-\sum_i\sigma^z_i\sigma^z_{i+1}-\sum_i\sigma^x_i$. Each dashed line is the largest entropy $\log M$ that an MPS with that bond dimension can hold. Look at how the curve crosses the lines for $M=2$, $M=4$ and $M=8$ in turn. It turns over at $t\approx4$ only because the chain is finite.](figures/web/session07/quench_entropy.svg){#sch:s07:quench_entropy alt="The entropy of half of a chain against time after a quench, rising about linearly and crossing three horizontal dashed lines for the bond dimensions 2, 4 and 8."}

![In two dimensions the boundary of a region grows with its size, so the number of cut bonds grows too. Look at panel (b), where doubling the linear size of $A$ doubles the number of cut bonds. An MPS that runs through the lattice cuts a line of this length, so its bond dimension must grow exponentially with the width of the system.](figures/s07f02_arealaw.svg){alt="A chain of dimers and a square lattice of tetramers, with the bonds cut by the boundary of a region drawn in red."}

::: quiz
After a sudden change of the Hamiltonian the entanglement of a chain grows linearly with time. Why is this a problem for an MPS with fixed $M$?

- [ ] The state stops being normalized after a quench.

    This is false. The evolution with a Hamiltonian is unitary, so $\langle\psi|\psi\rangle=1$ at all times. The norm is not what grows after a quench.

- [ ] The Hamiltonian becomes nonlocal after a quench.

    This is false. A quench only changes the parameters. For example $J=1$ becomes $J=2$ and the Hamiltonian is still a sum of nearest-neighbor terms.

- [x] The entropy soon exceeds $\log M$, so $M$ must grow exponentially with time.

    This is true. The bound [(7.10)](#eq-7-10) gives $S\le\log M$, and a linear growth of $S$ needs $M\sim e^{S}$ to grow exponentially. For this reason long-time dynamics is hard for MPS.

    ![The half-chain entropy after a quench passes each limit $\log M$ at a finite time.](figures/web/session07/quench_entropy.svg){alt="The entropy of half of a chain against time after a quench, rising about linearly and crossing horizontal dashed lines for the bond dimensions 2, 4 and 8."}

:::

::: quiz
Which of the following ground states is the hardest for an MPS with a fixed bond dimension?

- [ ] A gapped spin chain with 100 sites.

    This is false. The AKLT chain is gapped and its exact ground state is an MPS with $M=2$, for 100 sites or for 10000. The entropy of a gapped chain saturates.

- [x] A gapped spin model on a $10\times10$ square lattice.

    This is true. An MPS has to pass through the lattice, and its cut crosses a boundary of about ten bonds. The entropy is then ten times the one of a single bond, and the bond dimension that it needs is exponentially larger.

- [ ] A dimer product state with 100 sites.

    This is false. A product of dimers has a cut that crosses at most one singlet, with entropy $\log2$ at most. It is an exact MPS with $M=2$.
:::

::: notebookbox
**Notebook check-in:** [`session7.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session7.ipynb), "Entanglement entropy of the ground state" (Core), "Size dependence of the entanglement entropy" (Challenge), and "Bond dimension dependence of the entanglement entropy" (Challenge)

With these three exercises you can reproduce Sections [7.5](#sec-7-5) to [7.8](#sec-7-8) numerically. First, you compute the entanglement entropy at each bond for the MPS ground state of a Heisenberg chain. Then you check that it grows very little with the system size, which is the 1D area-law saturation of Section [7.6](#sec-7-6), but this time in a gapless chain and not in a gapped one. Finally, you check that it saturates once the bond dimension is large enough to satisfy [(7.10)](#eq-7-10). The quiz of the first exercise also asks you to replace the model with an Ising model and to see how the entropy changes. This is a quick way to see how the area law responds to a really different ground state, which in this case is classical and has zero entanglement.
:::

::: {.tryit notebook="session7.ipynb" cell="Bond dimension dependence of the entanglement entropy"}
Compare the curves of $L=10$ and $L=30$ as a function of `maxm`. Both curves follow the bound $\ln\chi$ at small $\chi$ and then saturate. Which chain saturates at the larger bond dimension, and why?
:::

::: comesback
- In Section [7.11](#sec-7-11) MERA describes the slow growth of the entropy at criticality, and PEPS are the network for two dimensions.
- In Section [10.3b](#sec-10-3b) neural network quantum states are a variational family that contains MPS and PEPS and imposes less structure on the state.
:::
