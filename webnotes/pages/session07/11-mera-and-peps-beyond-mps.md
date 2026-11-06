## MERA and PEPS beyond MPS {#sec-7-11 number="7.11"}

Matrix product states are the simplest member of a much larger family, which is called **tensor networks**. Nothing requires the tensors to sit in a 1D chain, and the same coefficient tensor $C$ of [(7.4)](#eq-7-4) can also be drawn as a 2D grid or as a general graph of connections. A richer connectivity makes the optimization harder, and MPS are the tensor network that is easiest to optimize, but in exchange it can represent a larger class of states. Let us mention two of these architectures.

The **multi-scale entanglement renormalization ansatz (MERA)** organizes its tensors in a hierarchy of length scales instead of along a single chain. This extra structure allows it to describe more entanglement than an MPS with a comparable number of parameters. This is important because the area law [(7.9)](#eq-7-9) is strictly a statement about *gapped* systems. At a critical point, which is a continuous quantum phase transition usually described by a conformal field theory in 1+1 dimensions, the entanglement entropy of the ground state does not saturate anymore. Instead, it grows logarithmically with the size of the subsystem,

$$S(\ell) \;=\; \frac{c}{3}\log \ell \;+\; \text{const.}, \tag{7.12}$$

where $c$ is the central charge of the CFT. This is a weak but real violation of the strict area law [(7.9)](#eq-7-9), and the extra hierarchical structure of MERA is built to describe this kind of weak violation. For this reason MERA is the tensor network that is used at criticality.

**Projected entangled pair states (PEPS)** are the direct 2D generalization of the MPS idea. Instead of tensors coupled in a line, the tensors sit on the nodes of a real 2D lattice, and they are coupled to all their lattice neighbors. This is a natural and promising architecture for 2D quantum many-body problems, but it has a real cost. For PEPS there is no analogue of the simple local eigenvalue problem for a single tensor that we have in DMRG, because the contraction of a general 2D tensor network is itself a hard computational problem. This is different from the 1D contraction, which is what made the local eigenvalue problem of Section [7.10](#sec-7-10) possible to solve. The optimization of PEPS is still an open and harder problem. Figure [7.6](#fig:s07:merapeps) shows both architectures, where the extra structure of each one comes from and what it costs.

![The two tensor networks beyond the chain, and what their geometry gives. Left, the multi-scale entanglement renormalization ansatz. Its tensors are stacked in layers. Each layer first removes the short-range entanglement between neighbouring blocks with the disentanglers, the boxes, and then it combines two sites into one with the triangular isometries, so the network describes the state at longer and longer length scales and not at successive positions along a chain. A division of the system, the red plane, now cuts one bond in every layer instead of one bond in total, and this is how MERA can describe the logarithmically growing entropy [(7.12)](#eq-7-12) of a critical chain, which an MPS with fixed bond dimension cannot reach. Right, projected entangled pair states, the direct 2D generalization of [(7.5)](#eq-7-5), with one tensor per lattice site that has a physical leg and four virtual bonds. The figure also shows the difficulty. There is no way to sweep along such a network one tensor at a time with the rest reduced to a simple environment, and the exact contraction of the network is itself a hard problem, which is why PEPS have no simple analogue of DMRG.](figures/s07f06_merapeps.svg){#fig:s07:merapeps number="7.6"}

::: quiz
A critical chain has $S(\ell)=\tfrac c3\log\ell$ with $c=1$. By how much does $S$ grow when the block goes from $\ell=10$ to $\ell=1000$?

- [ ] By zero, since the entropy saturates.
- [x] By about $1.5$, which is $\tfrac13\log100$.
- [ ] By about $150$, since $\ell$ grows by a factor of $100$.
- [ ] By about $3$, which is $\log 1000-\log 10$.

The difference is $\tfrac13\log(1000/10)=\tfrac13\log100\approx1.5$. The growth is real but slow, and this is why MPS with a moderate $M$ still work for a critical chain of moderate length.
:::

::: quiz
A cut of a MERA crosses one bond in every layer, and the number of layers grows as $\log\ell$ for a block of size $\ell$. What entropy can the cut hold?

- [ ] It is bounded by a constant, as in a gapped chain.
- [ ] It grows linearly with $\ell$, as in a volume law.
- [x] It can grow as $\log\ell$, which is the critical behavior [(7.12)](#eq-7-12).
- [ ] It is zero, since the layers cancel.

Each cut bond can hold at most $\log M$, so the sum over the layers is of order $\log\ell$ times $\log M$. An MPS has a single bond at the cut, and it cannot do this.
:::

This is also where the lecture of this year ends. In contrast with some previous editions of this course, the recording of this year stops after MERA and PEPS, and it does not continue with neural network quantum states. The single mention in Section [7.3](#sec-7-3) is all that we say about this topic in this session. The tensor-network methods built in Sections [7.4](#sec-7-4) to [7.11](#sec-7-11) are still important, since in session 10 we will use the same MPS, MERA and PEPS architectures directly as machine-learning classifiers, and we will come back to neural network quantum states in detail, from the point of view of machine learning.

::: notebookbox
**Notebook check-in:** [`session7.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session7.ipynb), "The entanglement entropy as a signal for phase transitions" (Challenge)

In this exercise you follow the entanglement entropy of the ground state of the transverse-field Ising chain while you change the transverse field across its quantum critical point, using the MPS methods of `dmrgpy`. Away from criticality you should see the area-law saturation of Section [7.8](#sec-7-8). Close to the transition, you should see that the entropy does not saturate, as predicted by [(7.12)](#eq-7-12). The quiz also asks which regime is the hardest for MPS, and this question asks you to connect back to the reason why MERA exists.
:::

::: {.tryit notebook="session7.ipynb" cell="The entanglement entropy as a signal for phase transitions"}
Run the loop over `Bx` for `L=40` and find the field where the entropy has its maximum. In these units the transition of the transverse-field Ising chain is at $B_x=0.5$, so the peak should sit close to it. Repeat for `L=20` and see how the peak changes.
:::
