## The hard case, the Ising gauge theory {#sec-10-6b number="10.6b"}

In the first part we saw that for the Ising model a local order parameter is enough. Let us now take a model where it is not.

**The hard case, the Ising gauge theory.** Now we replace the coupling between pairs with a **plaquette** interaction, which is the product of the four spins around each elementary square of the lattice,

$$H_{\rm IGT} = -J\sum_{p} \prod_{i \in \partial p} \sigma_i, \tag{10.10}$$

where the sum runs over the plaquettes $p$ and the product runs over the four spins on the four bonds around that plaquette. Note that here the spins live on the *links* of the lattice and not on its sites. At zero temperature the ground state satisfies $\prod_{i\in\partial p}\sigma_i =
+1$ on *every* plaquette, but this constraint is satisfied by a macroscopic number of different spin configurations. For instance, if we flip the four spins on the bonds that meet at a single vertex, every plaquette product stays the same, because each of the four plaquettes that touch this vertex contains exactly two of these four bonds and every other plaquette contains none of them. This local gauge transformation is what gives the model its name. At infinite temperature, instead, plaquettes with product $+1$ and $-1$ appear with equal probability. Both the ordered configurations, which satisfy the constraint, and the disordered ones can look, one by one, like a featureless $50/50$ mix of up and down spins. As a result, the naive order parameter [(10.9)](#eq-10-9), which worked perfectly for the Ising model, is *useless* here. The reason is that no local quantity can distinguish the two regimes, which is the same obstruction that forced sessions 3 and 4 to leave local order parameters and to use Chern numbers and Zak phases. What [(10.10)](#eq-10-10) reproduces, in a simple classical model, is this feature of those earlier examples. Note that in two dimensions this model has no true transition and no topological order at finite temperature, and only its ground state at zero temperature has topological order. On a finite system, however, the low-temperature and high-temperature regimes are clearly different, and no local quantity can distinguish them, which is what makes this model a good test for the classifier.

A convolutional neural network, trained on labeled configurations at low $T$ and high $T$ with the same supervised architecture as before, succeeds where the naive summary statistic fails. In practice, it learns a nonlocal function of the spin configuration, which plays the role that a topological invariant would play analytically. We should state one more physical point carefully, since it is easy to mix up. The two regimes here are separated by a **size-dependent crossover** and not by a true phase transition at finite temperature, so there is no sharp $T_c$ that the result converges to as the system grows, unlike the true Ising transition of [(10.9)](#eq-10-9). What makes the machine-learning result useful is that the trained network has only seen one system size during training, and it still captures this crossover correctly for *other* sizes and temperatures on which it was never trained. The slides show it trained at a single size and evaluated from $L = 4$ up to $L = 28$. Figure [10.5](#fig:s10:phaseclass) shows the easy and the hard case next to each other in real space, which is where the difference between them can be seen.

![Why one phase-classification problem is easy and the other is hard, seen from above with $\sigma=+1$ raised and $\sigma=-1$ sunk. **(a,b)** For the Ising model [(10.9)](#eq-10-9) the magnetization of a single snapshot already separates the phases, and a network trained on such snapshots only finds again the logic of a local order parameter of sessions 1, 5 and 6. **(c,d)** For the Ising gauge theory [(10.10)](#eq-10-10) the spins live on the *bonds*, and the $T=0$ condition $\prod_{i\in\partial p}\sigma_i = +1$ leaves an exponentially large degenerate manifold. A typical ground state is random from bond to bond, so the magnetization is $\approx 0$ in both columns and no quantity on a single bond can distinguish them. The difference is in the four-spin structure of the plaquettes, which is marked by a cross where the product is $-1$, and the convolutional network has to find by itself a function of the configuration that is sensitive to it. The shaded star in (c) is a gauge flip of the four bonds at one vertex, which keeps every plaquette product. This is the same obstruction that forced sessions 3 and 4 to go from local order parameters to Chern numbers and Zak phases.](figures/s10f05_phaseclassification.svg){#fig:s10:phaseclass number="10.5"}

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
