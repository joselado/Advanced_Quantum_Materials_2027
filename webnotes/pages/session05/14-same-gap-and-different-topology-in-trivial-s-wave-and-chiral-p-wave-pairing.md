## Same gap and different topology in trivial s-wave and chiral p-wave pairing {#sec-5-14 number="5.14"}

This is the central point of the whole session. Two superconducting gaps can have completely identical *spectral* properties, where both fully gap the Fermi surface with, for example, the same minimum gap, and still be topologically different. Let us compare plain s-wave pairing, $\Delta(\mathbf k) =
\Delta_0$, with **chiral p-wave** pairing,

$$\Delta_{p+ip}(\mathbf k) = \Delta_0\left(\sin k_x + i \sin k_y\right), \tag{5.15}$$

which is an odd-parity, spin-triplet order, in agreement with [(5.12)](#eq-5-12) since $\Delta_{p+ip}(-\mathbf
k) =
-\Delta_{p+ip}(\mathbf k)$, and which winds once around the origin of the complex plane as $\mathbf
k$ goes around the Fermi surface. Both [(5.9)](#eq-5-9) with $\Delta_0$ and [(5.9)](#eq-5-9) with $\Delta_{p+ip}$ can fully gap the same Fermi surface, so a measurement of the bulk gap alone cannot distinguish them. However, in the same way as for the Chern-number classification of gapped bands in the topological-band-structure session, we can compute the Chern number of the occupied BdG bands for each case, and the two results are completely different. The trivial s-wave state has Chern number $0$, while the chiral p-wave state has Chern number $\pm 2$, where the sign is set by the chirality, $p_x + ip_y$ or $p_x - ip_y$.

What distinguishes them, as shown in figure [5.4](#fig:s05:topology), is the winding of the *phase* of $\Delta(\mathbf k)$ when $\mathbf k$ goes once around the Fermi surface. This phase is constant for s-wave, and it makes one full turn for $p+ip$.

::: quiz
Both the $s$-wave and the $p+ip$ gap open the same gap on the same Fermi surface. Which quantity is different?

- [ ] The minimum energy of the bulk bands.

    This is false. Both gaps are the same on the same Fermi surface, since $E=|\Delta|$ there. For $|\Delta|=0.2t$ both give the minimum energy $0.2t$, so spectroscopy of the bulk cannot tell them apart.

- [x] The Chern number of the occupied BdG bands.

    This is true. The winding of the phase of $\Delta(\mathbf k)$ around the Fermi surface gives the Chern number. It is $0$ for $s$-wave pairing and $\pm2$ for chiral $p$-wave pairing.

- [ ] The number of Fermi pockets.

    This is false. The pockets belong to the normal state $\varepsilon(\mathbf k)$, which is the same in both cases. For a single pocket around $\Gamma$ both superconductors have exactly one.
:::

This has the consequence that we expect from the bulk-boundary correspondence. In a finite system, the s-wave superconductor stays gapped everywhere, both in the bulk and at the edge, in the same way as a trivial insulator with Chern number zero. The chiral p-wave superconductor, on the other hand, is gapped in the bulk but has gapless *chiral* edge modes. On one edge there are $|C|$ branches that all propagate in the same direction, here two, one from each of the two identical spin blocks, and the opposite edge has the same number of branches that propagate in the opposite direction, as a state with Chern number $\pm 2$ must have. So on a ribbon we see two sets of branches that propagate in opposite directions, but they are localized on opposite edges and do not share one edge. These edge modes turn out to be fractions of an electron in a very specific and exact sense, since they are Majorana modes, and the rest of this session is about what this means.

![Two gaps that a spectroscopy experiment cannot distinguish, seen from above. Each dial is the phase of $\Delta(\mathbf k)$, an arrow in the complex plane, drawn at the point of the Fermi pocket where it is evaluated. (a) For $s$-wave pairing this phase is the same everywhere, so as $\mathbf k$ goes once around the pocket the value of $\Delta$ stays at a single point of the complex plane, with winding number zero and Chern number zero. (b) For chiral $p$-wave pairing [(5.15)](#eq-5-15) the phase instead follows the direction of $\mathbf k$, so $\Delta$ draws a loop that encircles the origin once. The modulus is essentially the same in both cases, so both fully gap the same pocket by the same amount. Only the winding is different, and the winding is what the Chern number counts. (c) The consequence in a finite sample. The trivial state is gapped at its boundary as well as in its bulk, while the chiral state must have $|C|$ gapless branches on each edge, all going in the same direction, and in the opposite direction on the opposite edge. Here $C=\pm 2$, with one branch from each of the two identical spin blocks of [(5.8)](#eq-5-8).](figures/s05f04_topology.svg){#fig:s05:topology number="5.4"}

The edge of a Chern insulator, from the quantum Hall and topological sessions, is the model for what we expect here. The figure below shows it again.

![The chiral edge states of a Chern insulator. The chiral $p$-wave superconductor has the same structure, with Majorana branches instead of electron branches.](figures/s03f01_chiraledge.svg){alt="A gapped bulk with a chiral channel running along its edge, and a channel that goes around an impurity."}

::: quiz
We replace $p_x+ip_y$ by $p_x-ip_y$, and the bulk gap does not change. What happens to the edge modes of a ribbon?

- [ ] They disappear, since the order is no longer chiral.

    This is false. The order $p_x-ip_y$ is chiral too, with the opposite winding. Its Chern number is $-2$ and not $0$, so two edge branches are still required.

- [ ] They stay the same, since the gap is the same.

    This is false. The same gap does not fix the direction. The sign of the Chern number sets it, so a branch that moves right on the top edge now moves left.

- [x] The number of branches on an edge stays the same, and each of them runs in the opposite direction.

    This is true. The Chern number changes from $+2$ to $-2$. The number $|C|=2$ of branches does not change, and their direction on a given edge flips.
:::

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "Trivial and topological superconducting order parameters, bulk spectra" (Core), and "\...edge spectra" (Core)

Build the s-wave and chiral p-wave BdG Hamiltonians next to each other, and check that their bulk spectra look similar, since both are gapped with a comparable gap size. Then move to a ribbon geometry and check that only the p-wave case has gapless chiral edge states, with branches of opposite velocity on the two edges of the ribbon, which is the distinction driven by the Chern number of section [5.14](#sec-5-14).
:::

::: {.tryit notebook="session5.ipynb" cell="Trivial and topological superconducting order parameters, bulk spectra"}
In the cell, `plot_case("chiral_pwave",0.4)` writes the Chern number in the title. Change `0.4` to `0.8`. The Chern number keeps its magnitude 2 as long as the gap stays open, and the $s$-wave case keeps zero.
:::
