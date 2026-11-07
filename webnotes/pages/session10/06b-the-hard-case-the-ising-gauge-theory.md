## The hard case, the Ising gauge theory {#sec-10-6b number="10.6b"}

In the first part we saw that for the Ising model a local order parameter is enough. Let us now take a model where it is not.

**The hard case, the Ising gauge theory.** Now we replace the coupling between pairs with a **plaquette** interaction, which is the product of the four spins around each elementary square of the lattice,

$$H_{\rm IGT} = -J\sum_{p} \prod_{i \in \partial p} \sigma_i, \tag{10.10}$$

where the sum runs over the plaquettes $p$ and the product runs over the four spins on the four bonds around that plaquette. Note that here the spins live on the *links* of the lattice and not on its sites. At zero temperature the ground state satisfies $\prod_{i\in\partial p}\sigma_i =
+1$ on *every* plaquette, but this constraint is satisfied by a macroscopic number of different spin configurations. For instance, if we flip the four spins on the bonds that meet at a single vertex, every plaquette product stays the same, because each of the four plaquettes that touch this vertex contains exactly two of these four bonds and every other plaquette contains none of them. This local gauge transformation is what gives the model its name. A gauge field that lives on the links of the lattice also appeared in Section [8.10](#sec-8-10), where it emerged from the parton construction of a spin liquid. At infinite temperature, instead, plaquettes with product $+1$ and $-1$ appear with equal probability. Both the ordered configurations, which satisfy the constraint, and the disordered ones can look, one by one, like a featureless $50/50$ mix of up and down spins. As a result, the naive order parameter [(10.9)](#eq-10-9), which worked perfectly for the Ising model, is *useless* here. The reason is that no local quantity can distinguish the two regimes. This is the same obstruction that forced Session 3 and Session 4 to leave local order parameters and to use the Chern numbers of Section [3.5](#sec-3-5) and the Zak phases of Section [3.9c](#sec-3-9c). What [(10.10)](#eq-10-10) reproduces, in a simple classical model, is this feature of those earlier examples. Note that in two dimensions this model has no true transition and no topological order at finite temperature, and only its ground state at zero temperature has the topological order of Section [10.6](#sec-10-6). On a finite system, however, the low-temperature and high-temperature regimes are clearly different, and no local quantity can distinguish them, which is what makes this model a good test for the classifier.

A convolutional neural network, trained on labeled configurations at low $T$ and high $T$ with the same supervised architecture as before, succeeds where the naive summary statistic fails. In practice, it learns a nonlocal function of the spin configuration, which plays the role that a topological invariant would play analytically. We should state one more physical point carefully, since it is easy to mix up. The two regimes here are separated by a **size-dependent crossover** and not by a true phase transition at finite temperature. So there is no sharp $T_c$ that the result converges to as the system grows, unlike the true Ising transition of [(10.9)](#eq-10-9). What makes the machine-learning result useful is that the network has seen only one system size during training. It still captures this crossover correctly for *other* sizes and temperatures, on which it was never trained, and in the example of this session it is evaluated from $L = 4$ up to $L = 28$. Figure [10.5](#fig:s10:phaseclass) shows the easy and the hard case next to each other in real space, which is where the difference between them can be seen.

![Why one phase-classification problem is easy and the other is hard, seen from above with $\sigma=+1$ raised and $\sigma=-1$ sunk. **(a,b)** For the Ising model [(10.9)](#eq-10-9) the magnetization of a single snapshot already separates the phases. A network trained on such snapshots only finds again the logic of a local order parameter, as in Session 1, Session 5 and Session 6. **(c,d)** For the Ising gauge theory [(10.10)](#eq-10-10) the spins live on the *bonds*, and the $T=0$ condition $\prod_{i\in\partial p}\sigma_i = +1$ leaves an exponentially large degenerate manifold. A typical ground state is random from bond to bond, so the magnetization is $\approx 0$ in both columns and no quantity on a single bond can distinguish them. The difference is in the four-spin structure of the plaquettes, marked by a cross where the product is $-1$. The convolutional network has to find by itself a function of the configuration that is sensitive to it. The shaded star in (c) is a gauge flip of the four bonds at one vertex, which keeps every plaquette product. This is the same obstruction that forced Session 3 and Session 4 to go from local order parameters to Chern numbers and Zak phases.](figures/s10f05_phaseclassification.svg){#fig:s10:phaseclass number="10.5"}

![Histograms of $|m|$ for single snapshots on a $16\times16$ lattice, from Monte Carlo, at a low and at a high temperature. For the Ising model, on the left, with $k_BT=1.5J$ and $3.5J$, the two histograms do not overlap, so one number per snapshot separates the two regimes. For the Ising gauge theory, on the right, with $k_BT=0.2J$ and $5J$, the two histograms lie on top of each other at $|m|\approx0.04$. The gauge flips of the four bonds at a vertex cost no energy, and at low temperature they scramble the bonds as much as the heat does at high temperature. The difference sits in the plaquette products of Figure [10.5](#fig:s10:phaseclass), which the network has to find by itself.](figures/web/session10/igt_hist.svg){#sch:s10:igt_hist alt="Two histograms of the absolute magnetization. On the left a red histogram near zero and a blue spike near one. On the right the red and blue histograms lie on top of each other near zero."}

::: quiz
In the Ising gauge theory we flip the four bonds that meet at one vertex. How does this change the plaquette products?

- [ ] Two of the four plaquettes change sign.

    This is false. A plaquette changes sign only if one of its bonds is flipped, or three. Each plaquette of the star has exactly two flipped bonds, so none changes sign.

- [x] None of them changes, since each plaquette contains exactly two of the four bonds.

    This is true. Two flipped bonds in a plaquette give $(-1)^2=+1$. Each of the four plaquettes at the vertex has two of the four bonds, so no plaquette product changes.

- [ ] All four plaquettes change sign.

    This is false. Take one plaquette of the star. Two of its four bonds are flipped, so its product gets the factor $(-1)^2=+1$ and not $-1$. The same holds for the other three.
:::

::: quiz
The trained classifier for the gauge theory does not give a transition that becomes sharper as $L$ grows. Why?

- [ ] The network is too small to see the transition.

    This is false. The same convolutional network finds a sharp transition for the Ising model as $L$ grows, so its size is not the limit.

- [ ] The magnetization is a better order parameter at large $L$.

    This is false. For the gauge theory the magnetization is zero at all temperatures, since a vertex flip reverses the sign of every bond at the vertex and does not change the energy. It cannot be an order parameter at any $L$.

- [x] The two regimes are separated by a crossover and not by a phase transition at finite temperature.

    This is true. The two-dimensional model has order only at $T=0$. For an open lattice the plaquette average is $\tanh(J/T)$, which is smooth, so the crossover does not sharpen.
:::

::: comesback
- In Section [10.7](#sec-10-7) a network is trained on simulated data to infer a Hamiltonian, which is the last construction of the course.
- In Section [10.8](#sec-10-8) the split between local order parameters and topological invariants is one of the threads that join the whole course.
:::
