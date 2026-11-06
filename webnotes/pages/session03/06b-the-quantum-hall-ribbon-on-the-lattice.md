## The quantum Hall ribbon on the lattice {#sec-3-6b number="3.6b"}

Let us look at a concrete model. We take a tight-binding square lattice with a perpendicular magnetic field and cut it into a ribbon of finite width, which has translational invariance along the ribbon but is finite across it. When we diagonalize this ribbon, we find the structure described above. There are flat bulk bands similar to Landau levels, and there are dispersive edge branches that cross the gap, with one branch confined to each edge and propagating in only one direction. If we look at the low-energy region close to zero energy, the spacing between the flat bands approaches the equal spacing of a continuum two-dimensional electron gas in a magnetic field, so the tight-binding model reproduces the standard Landau problem in the appropriate limit. This computed band structure, with the bulk flat bands in green and the two edge branches that propagate in opposite directions, is shown on the slides but was only described qualitatively in the lecture. To reproduce it numerically is what the notebook box below asks you to do.

![The spectrum of a quantum Hall ribbon, from session 4. The flat bulk levels are the Landau levels. The branches that bend up near the walls are the edge states, one for each edge. This panel is computed in the continuum with hard walls, and the lattice ribbon of the notebook gives the same picture. Look at the number of branches that cross the chemical potential, the translucent plane.](figures/s04f01_ribbon.svg){panel="a" alt="Flat Landau levels of a ribbon with the edge branches that bend up near the walls and cross the gap."}

::: quiz
In the spectrum of the ribbon the bulk Landau levels are flat. What does this say about the current carried by the bulk states?

- [ ] They carry a current that is proportional to their energy.

    This is false. Compare the first and the fifth Landau level. Both are flat, so both have $\partial E/\partial k=0$, and neither carries current although their energies differ by a factor of nine.

- [x] They carry no current, since their group velocity $\partial E/\partial k$ is zero.

    This is true. The velocity along the ribbon is the slope of the band. A flat level has zero slope, so the current is carried only by the edge branches that cross the chemical potential.

- [ ] They carry the quantized Hall current.

    This is false. With the chemical potential in a gap, a voltage $V$ between the edges gives the current $C(e^2/h)V$ through the edge branches, which are the only states with a slope. The flat bulk levels have no slope and contribute nothing.

:::

::: notebookbox
**Notebook check-in:** [`session3.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session3.ipynb), "From electrons in a ribbon to the quantum Hall state" (Core), "The quantum Hall effect in graphene" (Core), and "Localization of the edge states in the quantum Hall effect" (Challenge)

Build a square-lattice ribbon, and then a honeycomb-lattice ribbon, with a magnetic field and reproduce the figure described above, with flat Landau-level bulk bands and chiral edge branches. Check the propagation direction of the edge states at positive and at negative energy on each edge, which is the chirality argument of Section [3.6](#sec-3-6). Then look at how the edge states localize in real space as a function of energy, and how this localization changes for a weaker field or a narrower ribbon.
:::

::: {.tryit notebook="session3.ipynb" cell="The quantum Hall effect in graphene"}
Change `h.add_orbital_magnetic_field(0.01)` to `-0.01` and run the cell again. The color gives the position across the ribbon. Follow the branch that is localized at one edge and crosses zero energy. Its slope changes sign when the field is reversed, as in the figure of Section [3.6](#sec-3-6).
:::
